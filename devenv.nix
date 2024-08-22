{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [git poetry ruff];

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $GREET
  '';

  languages.python = {
    poetry = {
      enable = true;
      activate.enable = true;
      install.enable = true;
    };
  };

  enterShell = ''
    hello
    git --version
  '';

  # # https://devenv.sh/tests/
  # enterTest = ''
  #   echo "Running tests"
  #   git --version | grep --color=auto "${pkgs.git.version}"
  # '';

  pre-commit.hooks.shellcheck.enable = true;
}
