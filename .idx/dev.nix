{ pkgs, ... }: {
  # See https://developers.google.com/idx/guides/customize-idx-env
  channel = "stable-24.05"; # or "unstable"
  packages = [
    pkgs.python3
    pkgs.python312Packages.pip
  ];
  idx = {
    extensions = [ "ms-python.python" ];
    workspace = {
      onCreate = {
        
      };
      onStart = {
        pip-install = "pip install -r /home/user/new/requirements.txt";
        start-app = "python app.py &";
        start-bot = "python bot_server.py &";
      };
    };
  };
}
