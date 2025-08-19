import json, pathlib, typer
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = typer.Typer(add_completion=False)
ROOT = pathlib.Path(__file__).resolve().parent
DOMAINS_DIR = ROOT / "domains"
TEMPLATES_DIR = ROOT / "templates"

def load_domain_config(domain: str) -> dict:
    p = DOMAINS_DIR / f"{domain}.json"
    if not p.exists():
        raise typer.BadParameter(f"Unsupported domain: {domain}")
    return json.loads(p.read_text(encoding="utf-8"))

def render_templates(context: dict, out_dir: pathlib.Path):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape()
    )
    files = [
        ("backend/Dockerfile.j2", "Dockerfile"),
        ("backend/requirements.txt.j2", "requirements.txt"),
        ("backend/README.md.j2", "README.md"),
        ("backend/app/__init__.py.j2", "app/__init__.py"),
        ("backend/app/db.py.j2", "app/db.py"),
        ("backend/app/models.py.j2", "app/models.py"),
        ("backend/app/crud.py.j2", "app/crud.py"),
        ("backend/app/routers.py.j2", "app/routers.py"),
        ("backend/app/main.py.j2", "app/main.py"),
    ]
    for src, dst in files:
        tpl = env.get_template(src)
        content = tpl.render(**context)
        dst_path = out_dir / dst
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        dst_path.write_text(content, encoding="utf-8")
    (out_dir / "data").mkdir(exist_ok=True)

def _generate(domain: str, out: str):
    config = load_domain_config(domain)
    out_dir = pathlib.Path(out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    context = {"domain": domain, **config}
    render_templates(context, out_dir)
    typer.echo(f"Generated {domain} backend at: {out_dir}")

@app.command("generate")
def generate_cmd(
    domain: str = typer.Option(..., "--domain", help="Domain: healthcare, real_estate, ecommerce, education, freelancers"),
    out: str = typer.Option(..., "--out", help="Output directory"),
):
    _generate(domain, out)

# also support running WITHOUT the subcommand
@app.callback(invoke_without_command=True)
def default(
    ctx: typer.Context,
    domain: str = typer.Option(None, "--domain"),
    out: str = typer.Option(None, "--out"),
):
    if ctx.invoked_subcommand is None:
        if not domain or not out:
            typer.echo(
                "Usage:\n"
                "  python -m generator.cli generate --domain <domain> --out <path>\n"
                "  (or)\n"
                "  python -m generator.cli --domain <domain> --out <path>"
            )
            raise typer.Exit(code=1)
        _generate(domain, out)

if __name__ == "__main__":
    app()
