#!/usr/bin/env python3
"""
backup_zip.py — простой бэкап-пакер.
Примеры:
  python src/backup_zip.py --src .               # упаковать репозиторий (кроме .git и др.)
  python src/backup_zip.py --src . --out ..\repo_backup.zip
  python src/backup_zip.py --src C:\Data --exclude ".git,__pycache__,.venv,node_modules,dist,build"
"""
import argparse, os, sys, zipfile, datetime

DEFAULT_EXCLUDES = {".git", "__pycache__", ".venv", "node_modules", "dist", "build"}

def should_exclude(path_parts, excludes):
    # Исключаем, если любая часть пути совпала с исключением
    return any(part in excludes for part in path_parts)

def zip_dir(src_dir, out_path, excludes):
    src_dir = os.path.abspath(src_dir)
    out_path = os.path.abspath(out_path)

    if not os.path.isdir(src_dir):
        raise FileNotFoundError(f"Источник не найден или не папка: {src_dir}")

    # Чтобы не заархивировать сам архив
    def is_output_file(file_path):
        try:
            return os.path.samefile(file_path, out_path)
        except FileNotFoundError:
            return False

    total_files = 0
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            # Фильтруем каталоги на лету
            parts = os.path.relpath(root, src_dir).split(os.sep)
            if parts == ['.']:
                parts = []
            dirs[:] = [d for d in dirs if not should_exclude(parts + [d], excludes)]
            # Добавляем файлы
            for name in files:
                file_path = os.path.join(root, name)
                rel_parts = parts + [name]
                if should_exclude(rel_parts, excludes):
                    continue
                if is_output_file(file_path):
                    continue
                arcname = os.path.relpath(file_path, src_dir)
                zf.write(file_path, arcname)
                total_files += 1
    return total_files

def main():
    parser = argparse.ArgumentParser(description="Упаковать папку в ZIP с пропуском служебных каталогов")
    parser.add_argument("--src", required=True, help="Папка-источник (например, .)")
    parser.add_argument("--out", help="Путь к архиву .zip (по умолчанию: рядом с src, с таймстемпом)")
    parser.add_argument("--exclude", help="Список исключений через запятую", default="")
    args = parser.parse_args()

    excludes = set(x.strip() for x in args.exclude.split(",") if x.strip())
    excludes |= DEFAULT_EXCLUDES

    src_dir = args.src
    if args.out:
        out_path = args.out
    else:
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base = os.path.basename(os.path.abspath(src_dir)) or "backup"
        parent = os.path.dirname(os.path.abspath(src_dir)) or "."
        out_path = os.path.join(parent, f"{base}_{ts}.zip")

    total = zip_dir(src_dir, out_path, excludes)
    print(f"OK: заархивировано файлов: {total}")
    print(f"Архив: {out_path}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
