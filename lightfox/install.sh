#!/bin/bash
# Install a packaged LightFox build for the current user. Needs no root.
# Usage: lightfox/install.sh [path/to/lightfox-*.tar.*]
set -euo pipefail

src_dir="$(cd "$(dirname "$0")/.." && pwd)"
tarball="${1:-$(ls -t "$src_dir"/obj-lightfox/dist/lightfox-*.tar.* | head -1)}"
prefix="$HOME/.local/opt"
target="$prefix/lightfox"
staging="$prefix/.lightfox-new"

mkdir -p "$prefix" "$HOME/.local/bin" "$HOME/.local/share/applications"
rm -rf "$staging"
mkdir -p "$staging"
tar -xf "$tarball" -C "$staging" --strip-components=1
test -x "$staging/lightfox"

rm -rf "$target"
mv "$staging" "$target"
ln -sfn "$target/lightfox" "$HOME/.local/bin/lightfox"

for size in 16 22 24 32 48 64 128 256; do
  dir="$HOME/.local/share/icons/hicolor/${size}x${size}/apps"
  mkdir -p "$dir"
  cp "$src_dir/browser/branding/lightfox/default$size.png" "$dir/lightfox.png"
done

cat > "$HOME/.local/share/applications/lightfox.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=LightFox
GenericName=Web Browser
Comment=Firefox without the extras
Exec=$target/lightfox %u
Icon=lightfox
Terminal=false
StartupWMClass=lightfox
Categories=Network;WebBrowser;
MimeType=text/html;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
Actions=new-window;new-private-window;

[Desktop Action new-window]
Name=New Window
Exec=$target/lightfox --new-window %u

[Desktop Action new-private-window]
Name=New Private Window
Exec=$target/lightfox --private-window %u
EOF

command -v update-desktop-database >/dev/null && update-desktop-database "$HOME/.local/share/applications" || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -t "$HOME/.local/share/icons/hicolor" || true

echo "Installed LightFox to $target"
