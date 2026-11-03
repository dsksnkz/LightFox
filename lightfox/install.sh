#!/bin/bash
# Install a packaged LightFox build for the current user. Needs no root.
# Usage: lightfox/install.sh [path/to/package.tar.*]
set -euo pipefail

src_dir="$(cd "$(dirname "$0")/.." && pwd)"
tarball="${1:-$(ls -t "$src_dir"/obj-lightfox/dist/lightfox-*.tar.* | head -1)}"
prefix="$HOME/.local/opt"
target="$prefix/lightfox"
staging="$prefix/.lightfox-new"
profile="$HOME/.local/share/lightfox/profile"
launcher="$HOME/.local/bin/lightfox"

mkdir -p "$prefix" "$HOME/.local/bin" "$HOME/.local/share/applications" "$profile"
rm -rf "$staging"
mkdir -p "$staging"
tar -xf "$tarball" -C "$staging" --strip-components=1

binary=lightfox
test -x "$staging/$binary" || binary=firefox
test -x "$staging/$binary"

rm -rf "$target"
mv "$staging" "$target"

rm -f "$launcher"
cat > "$launcher" <<EOF
#!/bin/sh
exec "$target/$binary" --class lightfox --name lightfox --profile "$profile" "\$@"
EOF
chmod +x "$launcher"

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
Exec=$launcher %u
Icon=lightfox
Terminal=false
StartupWMClass=lightfox
Categories=Network;WebBrowser;
MimeType=text/html;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
Actions=new-window;new-private-window;

[Desktop Action new-window]
Name=New Window
Exec=$launcher --new-window %u

[Desktop Action new-private-window]
Name=New Private Window
Exec=$launcher --private-window %u
EOF

command -v update-desktop-database >/dev/null && update-desktop-database "$HOME/.local/share/applications" || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -t "$HOME/.local/share/icons/hicolor" || true

echo "Installed LightFox to $target"
