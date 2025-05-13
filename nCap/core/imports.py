from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends           import default_backend
from fastapi                                import FastAPI, APIRouter, Request, Depends, HTTPException
from fastapi.responses                      import JSONResponse, FileResponse
from fastapi.middleware.cors                import CORSMiddleware

# captcha
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import uvicorn
import hashlib
import base64
import random
import string
import hmac
import math
import json
import os
