{
  description = "Python application packaged using poetry2nix";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      p2nix = poetry2nix.lib.mkPoetry2Nix {inherit pkgs;};
    in {
      packages = {
        default = self.packages.${system}.gordi-agent;
        gordi-agent = p2nix.mkPoetryApplication {
          projectDir = self;
          overrides = p2nix.overrides.withDefaults (self: super: {
            paho-mqtt = super.paho-mqtt.overridePythonAttrs (old: {
              buildInputs = old.buildInputs or [] ++ [super.hatchling];
            });
          });
        };
      };
    });
}
