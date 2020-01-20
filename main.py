from src.App import App

if __name__ == '__main__':
    app = App()
    try:
        app.main()
    except KeyboardInterrupt:
        pass
    finally:
        pass
