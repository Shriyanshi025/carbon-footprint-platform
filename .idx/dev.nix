{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = [
    pkgs.python311
    pkgs.nodejs_20
  ];

  idx.workspace = {
    onCreate = {
      create-venv = ''
        python3 -m venv backend/venv
        source backend/venv/bin/activate
        pip install -r backend/requirements.txt
        npm install --prefix frontend
      '';
    };
    onStart = {
      activate-venv = ''
        source backend/venv/bin/activate
      '';
    };
  };
}