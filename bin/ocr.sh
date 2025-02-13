for img in *.jpg; do
    tesseract "$img" "text/$(basename "${img%.jpg}")" -l nld
done