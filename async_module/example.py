import asyncio

from async_module.runner import AsyncSyncRunner, async_to_sync


# 시크릿 매니저 예제
async def fetch_secret(secret_name: str) -> dict:
    await asyncio.sleep(1)
    return {"SecretString": f"secret-value-for-{secret_name}"}


# 동기 코드에서 직접 AsyncSyncRunner.run 사용
def get_secret_sync(secret_name: str) -> dict:
    return AsyncSyncRunner.run(fetch_secret(secret_name))


# 데코레이터를 사용하여 비동기 함수를 동기 함수로 변환
@async_to_sync
async def get_secret_sync_v2(secret_name: str) -> dict:
    return await fetch_secret(secret_name)


def get_database_uri() -> str:
    app_env = "PROD"
    if app_env == "PROD":
        secret = get_secret_sync("prod/secret")
        # secret = get_secret_sync_v2("prod/secret")
        secret_str = secret.get("SecretString", "")
        return f"postgresql://user:password@host:port/{secret_str}"
    else:
        import os

        return os.getenv("DATABASE_URI", "")


if __name__ == "__main__":
    uri = get_database_uri()
    print("Database URI:", uri)
