{
  pkgs ? import <nixpkgs> { },
}:

let
  nur =
  pkgs.nur or
  (
    import (builtins.fetchTarball "https://github.com/nix-community/NUR/archive/main.tar.gz") {
      inherit pkgs;
      repoOverrides = {
        milahu = import (pkgs.fetchFromGitHub {
            owner = "milahu";
            repo = "nur-packages";
            rev = "2d2ec41f5f1a416442321a0383f34b31e79b3bc3";
            hash = "sha256-Dd0kX0ey0A/IQcKyuxZ63mnjUTopwSaV8tMu3krsvAY=";
            fetchSubmodules = true;
          }) { inherit pkgs; };
      };
    }
  );
in

pkgs.mkShell {
  buildInputs = with pkgs; [
    diffutils
    tinyxxd
    nur.repos.milahu.kaitai-struct-compiler
    (python3.withPackages (pp: with pp; [
      # requests
      nur.repos.milahu.python3.pkgs.kaitaistruct
    ]))
  ];
}
