from fastapi import APIRouter

test_router = APIRouter()


@test_router.get("/healthz")
def health_check() -> dict[str, bool]:
    return {"success": True}


@test_router.get("/test")
def pdf_lib_test() -> dict[str, bool]:
    import locale
    import os
    from pathlib import Path

    # macOS 환경변수 설정
    os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib:" + os.environ.get(
        "DYLD_LIBRARY_PATH", ""
    )
    import ghostscript

    project_root = Path(__file__).resolve().parent
    input_file = project_root / "input.pdf"

    if not input_file.exists():
        return {"success": False, "error": f"File not found: {input_file}"}

    quality_settings = {
        "screen": "/screen",  # lower quality, smaller size, 72 dpi
        "ebook": "/ebook",  # low quality, 150 dpi
        "printer": "/printer",  # high quality, 300 dpi
        "prepress": "/prepress",  # high quality, color preserving, 300 dpi
        "default": "/default",  # selects versatile output at the cost of larger file size
    }
    quality = "ebook"

    args = [
        "gs",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=pdfwrite",
        f"-dPDFSETTINGS={quality_settings[quality]}",
        # "-sOutputFile=" + "test.pdf",
        "-o",
        "test.pdf",
        "-f",
        str(input_file),
    ]
    # encoding = locale.getpreferredencoding()
    # args = [a.encode(encoding) for a in args]

    ghostscript.Ghostscript(*args)
    return {"success": True}
