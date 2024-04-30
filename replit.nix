{ pkgs }: {
    deps = [
      pkgs.systemd
      pkgs.mysql
      pkgs.vim
      pkgs.cowsay
    ];
}