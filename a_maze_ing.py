import sys
sys.path.append('.')
sys.path.append('src')


def main() -> None:
    from main import dp
    dp.run(refresh_per_second=60)


if __name__ == "__main__":
    main()
