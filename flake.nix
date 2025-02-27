{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          python312
        ];

      shellHook = ''
        echo "Welcome to the nix shell"
        python --version
        VENV_DIR=venv
        if [ ! -d "$VENV_DIR" ]; then
           python -m venv $VENV_DIR
        fi
        source ./venv/bin/activate
      '';
      };
    };
}
