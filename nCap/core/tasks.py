from core.imports import APIRouter, JSONResponse, HTTPException, FileResponse, os, Path, json
from core.utils   import utility
from core.obf     import obfuscator
from core.captcha import cap

router  = APIRouter()
utils   = utility()
captcha = cap()

obf     = obfuscator(
            os.urandom(32)
        )

# RETURN CAPTCHA IMAGE
@router.get("/captcha")
def get_captcha_image(img: str):
    image_path = Path(f"core/solutions/{img}/captcha.png")

    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Server Error (img not found)")

    return FileResponse(path=image_path, media_type="image/png", filename="captcha.png")
# END

@router.get("/createTask")
def create_task():

    id     = utils.createId(64)
    taskId = obf.obfuscate(id)

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "taskId": taskId
            }
        }
    )

@router.get("/getCaptcha")
def get_captcha(taskId: str):
    id = obf.deobfuscate(taskId)
    if not id:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": {
                    "error": "Invalid data"
                }
            }
        )

    else:
        path = Path(f"core/solutions/{id}")
        path.mkdir(parents=True, exist_ok=True)

        captcha_code = utils.createId(6)

        imgpath      = path / "captcha.png"
        if not imgpath.exists():
            img  =  captcha.create(captcha_code)
            img.save(imgpath)

        data = {
            "solution": captcha_code,
        }

        with open(path / "solution.json", "w") as f:
            json.dump(data, f, indent=4)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "img": f"http://127.0.0.1:1337/api/captcha?img={id}"
                }
            }
        )
    
@router.get("/solve")
def solve_captcha(taskId: str, solved: str):
    id = obf.deobfuscate(taskId)
    captcha = Path(f"core/solutions/{id}/solution.json")
    if not captcha.exists():
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": {
                    "error": "Invalid captcha"
                }
            }
        )

    try:
        with open(captcha, "r") as f:
            solution_data = json.load(f)

        correct_solution  = solution_data.get("solution")
        is_correct        = (solved == correct_solution)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "correct": is_correct
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": {
                    "error": f"Failed to check solution."
                }
            }
        )
