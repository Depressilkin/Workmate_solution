from models import Loader, parser

if __name__ == '__main__':
    execute = parser.parse_args()
    loader = Loader()
    loader.load_log(execute.file)
    loader.render_average()
