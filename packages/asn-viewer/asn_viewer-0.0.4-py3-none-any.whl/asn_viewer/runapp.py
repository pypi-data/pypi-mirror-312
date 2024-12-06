from pathlib import Path

from .asn_decoder import ASNDecoder
from .asn_viewer_config import ASNViewerConfig, ASNViewerCmdArguments


def main():
    arg_parser = ASNViewerCmdArguments()
    try:

        args = arg_parser.parse_args()

        conf = ASNViewerConfig(Path(args.config)) if args.config else None

        decoder = ASNDecoder(args.definition or conf.definition, args.object_name or conf.object_name)
        decoder.load_files(args.files or conf.files or tuple())

        if args.output or conf:
            decoder.save_decoded_to_file(Path(args.output or conf.output or '.'), args.search or conf.search or None)
        else:
            decoder.print_file_data_json(args.search or conf.search or None)

    except AttributeError as e:
        arg_parser.print_help()
        arg_parser.exit(1, f'Missing parameter: {e.name.replace("_", "-")}\n' )

    except KeyError as ke:
        arg_parser.exit(2, f'Field name {ke} is not in the ASN object definition\n' )

