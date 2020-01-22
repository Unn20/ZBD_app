from src.App import App

if __name__ == '__main__':
    app = App("config.json")
    try:
        app.main()
    except KeyboardInterrupt:
        pass
    finally:
        pass
