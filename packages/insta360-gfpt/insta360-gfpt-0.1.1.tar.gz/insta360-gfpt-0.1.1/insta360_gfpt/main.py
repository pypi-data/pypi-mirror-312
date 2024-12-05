import argparse

def main():
    parser = argparse.ArgumentParser(description='My Python Library CLI Tool')
    parser.add_argument('command', type=str, help='The command to execute')
    parser.add_argument('--option', type=str, help='An optional argument')

    args = parser.parse_args()

    if args.command == 'hello':
        print(f"Hello, {args.option}!")
    elif args.command == 'info':
        print(f"Info: {args.option}")
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()