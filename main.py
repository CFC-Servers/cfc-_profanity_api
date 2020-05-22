from aiohttp import web
from base64 import b64decode
from dotenv import load_dotenv
from os import getenv
from profanity_check import predict, predict_prob

load_dotenv()
ALLOWED_API_KEYS = getenv("ALLOWED_API_KEYS") or {"test"}

routes = web.RouteTableDef()

@routes.get("/probability/{b64}/{key}")
async def rating(request):
    key = request.match_info.get("key", "")

    if key not in ALLOWED_API_KEYS:
        return web.Response(status=401)

    data = request.match_info.get("b64", "")
    data = b64decode(data)

    return web.Response(body=str(predict_prob([data])[0]).encode("utf-8"))

app = web.Application()
app.router.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=8182)
