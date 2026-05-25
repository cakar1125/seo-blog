#!/usr/bin/env python3
"""GitHub Actions agent runner - Anthropic API + Jina web tools."""
import os, sys, subprocess, urllib.parse, glob

try:
    import anthropic
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "anthropic", "-q"], check=True)
    import anthropic


def web_search(query):
    encoded = urllib.parse.quote(query)
    r = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", "-H", "Accept: text/plain",
         f"https://s.jina.ai/{encoded}"],
        capture_output=True, text=True
    )
    return (r.stdout or "Sonuç bulunamadı")[:6000]


def fetch_url(url):
    r = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", f"https://r.jina.ai/{url}"],
        capture_output=True, text=True
    )
    return (r.stdout or "Sayfa alınamadı")[:6000]


def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Yazıldı: {path}"


def read_file(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return f"Dosya bulunamadı: {path}"


def list_files(directory="."):
    files = glob.glob(f"{directory}/**/*", recursive=True)
    return "\n".join(f for f in sorted(files) if os.path.isfile(f))[:3000]


TOOLS = [
    {
        "name": "web_search",
        "description": "Web'de arama yap",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "fetch_url",
        "description": "URL içeriğini al",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"],
        },
    },
    {
        "name": "write_file",
        "description": "Dosyaya yaz",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "read_file",
        "description": "Dosyayı oku",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "list_files",
        "description": "Klasördeki dosyaları listele",
        "input_schema": {
            "type": "object",
            "properties": {"directory": {"type": "string"}},
            "required": [],
        },
    },
]


def handle_tool(name, inputs):
    if name == "web_search":
        return web_search(inputs["query"])
    if name == "fetch_url":
        return fetch_url(inputs["url"])
    if name == "write_file":
        return write_file(inputs["path"], inputs["content"])
    if name == "read_file":
        return read_file(inputs["path"])
    if name == "list_files":
        return list_files(inputs.get("directory", "."))
    return f"Bilinmeyen araç: {name}"


def main():
    if len(sys.argv) < 2:
        print("Kullanim: python run_agent.py <prompt_dosyasi>")
        sys.exit(1)

    prompt_file = sys.argv[1]
    if not os.path.exists(prompt_file):
        print(f"Prompt dosyasi bulunamadi: {prompt_file}")
        sys.exit(1)

    with open(prompt_file, encoding="utf-8") as f:
        prompt = f.read()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("HATA: ANTHROPIC_API_KEY bulunamadi!")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    messages = [{"role": "user", "content": prompt}]
    print(f"Agent baslatildi: {prompt_file}")

    for _ in range(30):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            print("Tamamlandi.")
            break

        if response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    val = list(block.input.values())[0] if block.input else ""
                    preview = str(val)[:80]
                    print(f"  -> {block.name}({preview})")
                    result = handle_tool(block.name, block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    })
            messages.append({"role": "user", "content": results})
        else:
            print(f"Beklenmeyen stop_reason: {response.stop_reason}")
            break


if __name__ == "__main__":
    main()
