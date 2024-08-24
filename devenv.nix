{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = with pkgs; [git poetry ruff];

  env = {
    BROKER_IP = "gordi.agent.lab";
    BROKER_PORT = 1883;
    BROKER_USER = "mosquitto";
    BROKER_PASS = "arstarst";
  };

  languages.python = {
    enable = true;
    # version = "3.11.3";
    uv.enable = true;
    poetry = {
      enable = true;
      activate.enable = true;
      install.enable = true;
    };
  };

  enterShell = ''
    echo "Building Gordi..."
  '';

  pre-commit.hooks = {
    ruff.enable = true;
  };
}
