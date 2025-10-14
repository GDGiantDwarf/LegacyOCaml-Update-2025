# geneweb/cli/parser.py
import argparse

class GenewebCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="geneweb",
            description="GeneWeb Python - server and genealogy tools",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        self._add_global_options()
        self._add_server_options()
        self._add_security_options()
        self._add_misc_options()

    # --- GLOBAL ---
    def _add_global_options(self):
        g = self.parser.add_argument_group("Global options")
        g.add_argument("-version", action="store_true", help="Print the GeneWeb version and exit")
        g.add_argument("-hd", help="Root directory containing etc/, images/, lang/", default="gw")
        g.add_argument("-etc_prefix", help="Directory for etc/", default=None)
        g.add_argument("-bd", "--base-dir", help="Directory where databases are installed", default="bases")
        g.add_argument("-lang", help="Default language", default="fr")
        g.add_argument("-blang", action="store_true", help="Select language according to browser")
        g.add_argument("-p", "--port", type=int, default=2317, help="HTTP listening port")
        g.add_argument("-a", "--address", default="0.0.0.0", help="Listening IP address")

    # --- SERVER ---
    def _add_server_options(self):
        s = self.parser.add_argument_group("Server options")
        s.add_argument("-daemon", action="store_true", help="Unix daemon mode")
        s.add_argument("-cgi", action="store_true", help="Force CGI mode")
        s.add_argument("-cgi_secret_salt", help="Secret salt to secure CGI forms")
        s.add_argument("-conn_tmout", type=int, default=120, help="Connection timeout (Unix)")
        s.add_argument("-n_workers", type=int, default=20, help="Number of workers")
        s.add_argument("-max_pending_requests", type=int, default=150, help="Maximum pending requests")
        s.add_argument("-cache_in_memory", help="Database to preload in memory")
        s.add_argument("-cache_langs", nargs="*", help="Languages to preload in cache")
        s.add_argument("-only", help="Only authorized address")
        s.add_argument("-redirect", help="Redirect service to another address")

    # --- SECURITY ---
    def _add_security_options(self):
        sec = self.parser.add_argument_group("Security options")
        sec.add_argument("-auth", help="Authorization file (user:password)")
        sec.add_argument("-digest", action="store_true", help="Enable HTTP Digest Auth")
        sec.add_argument("-friend", help="Friend account password")
        sec.add_argument("-wizard", help="Wizard account password")
        sec.add_argument("-wjf", action="store_true", help="Downgrade wizard to friend")
        sec.add_argument("-login_tmout", type=int, default=1800, help="Login session timeout (CGI)")
        sec.add_argument("-trace_failed_passwd", action="store_true", help="Log failed passwords")

    # --- LOG / DEBUG ---
    def _add_misc_options(self):
        m = self.parser.add_argument_group("Logs and debugging")
        m.add_argument("-log", help="Log file ('-' for stdout)")
        m.add_argument("-log_level", type=int, default=6, help="Verbosity level (0–6)")
        m.add_argument("-debug", action="store_true", help="Enable debug mode")
        m.add_argument("-predictable_mode", action="store_true", help="Disable randomness for testing")
        m.add_argument("-robot_xcl", help="Exclude robots: <CNT>,<SEC>")
        m.add_argument("-min_disp_req", type=int, default=6, help="Minimum requests to log robot activity")
        m.add_argument("-max_clients", type=int, help="Maximum simultaneous clients (deprecated)")

    def run(self):
        args = self.parser.parse_args()

        if args.version:
            from geneweb import __version__
            print(f"GeneWeb Python {__version__}")
            return

        import uvicorn

        print(f"🚀 Starting GeneWeb server on {args.address}:{args.port}")
        print(f"📂 Base directory: {args.base_dir}")
        print(f"🌐 Default language: {args.lang}")

        # --- If debug or workers > 1, pass import string to uvicorn ---
        if args.debug or (args.n_workers and args.n_workers > 1):
            import_string = "geneweb.web.server:create_app"
            uvicorn.run(
                import_string,
                host=args.address,
                port=args.port,
                reload=args.debug,
                workers=args.n_workers or 1,
                log_level="debug" if args.debug else "info",
                factory=True,
            )
        else:
            from geneweb.web.server import create_app
            app = create_app(base_dir=args.base_dir, lang=args.lang)
            uvicorn.run(
                app,
                host=args.address,
                port=args.port,
                log_level="debug" if args.debug else "info",
            )
