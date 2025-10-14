# geneweb/cli/parser_minimal.py
import argparse
import uvicorn

class GenewebSetupCLI:
    """
    Minimal GeneWeb CLI with core server options.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="geneweb",
            description="GeneWeb Python - minimal server options",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        self._add_minimal_options()

    def _add_minimal_options(self):
        g = self.parser.add_argument_group("Core server options")
        g.add_argument("-bd", "--base-dir", help="Directory where the databases are installed.", default="bases")
        g.add_argument("-bindir", help="Binary directory (default = value of option -gd)", default=None)
        g.add_argument("-daemon", action="store_true", help="Unix daemon mode (runs in background)")
        g.add_argument("-gd", help="gwsetup directory", default="gw")
        g.add_argument("-gwd_p", type=int, help="Specify the port number of gwd (default = 2317); > 1024 for normal users.", default=2317)
        g.add_argument("-lang", help="Default language", default="fr")
        g.add_argument("-only", help="File containing the only authorized address", default=None)
        g.add_argument("-p", "--port", type=int, help="Select a port number (default = 2316); > 1024 for normal users.", default=2316)

    def run(self):
        args = self.parser.parse_args()

        # Print selected options
        print(f"🚀 Starting GeneWeb server on http://0.0.0.0:{args.port}")
        print(f"📂 Base directory: {args.base_dir}")
        print(f"🌐 Default language: {args.lang}")
        if args.daemon:
            print("⚡ Running in daemon mode (background process)")
        if args.only:
            print(f"🔒 Restricting access to addresses listed in {args.only}")

        # --- Run FastAPI server ---
        try:
            from geneweb.web.admin_server import create_app
        except ImportError:
            raise ImportError("Cannot import create_app from geneweb.web.server")

        app = create_app(base_dir=args.base_dir, lang=args.lang)

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=args.port,
            log_level="info",
        )
