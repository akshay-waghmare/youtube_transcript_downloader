"""Command-line interface for yttranscript."""

import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .core import TranscriptExtractor
from .models import Video
from .formatters import FormatType, get_formatter
from .exceptions import (
    YttranscriptError,
    InvalidUrlError,
    TranscriptNotAvailableError,
    LanguageNotFoundError,
    NetworkError,
    FileOutputError,
)


@click.command()
@click.argument('url', required=True)
@click.option(
    '--format', 
    'output_format',
    type=click.Choice(['plain', 'markdown'], case_sensitive=False),
    default='plain',
    help='Output format (default: plain)'
)
@click.option(
    '--output', 
    'output_file',
    type=click.Path(),
    help='Output file path (default: stdout)'
)
@click.option(
    '--language', 
    'language_code',
    help='Transcript language code (e.g., en, es, fr). Defaults to English, then first available.'
)
@click.option(
    '--timestamps/--no-timestamps',
    default=False,
    help='Include timestamps in output (default: no timestamps)'
)
@click.option(
    '--list-languages',
    'list_languages',
    is_flag=True,
    help='List available transcript languages for the video'
)
@click.option(
    '--force',
    is_flag=True,
    help='Overwrite existing output files without confirmation'
)
@click.version_option(version=__version__)
@click.help_option('-h', '--help')
def main(
    url: str,
    output_format: str,
    output_file: Optional[str],
    language_code: Optional[str],
    timestamps: bool,
    list_languages: bool,
    force: bool
) -> None:
    """Extract transcript from YouTube video.
    
    URL can be a full YouTube URL (youtube.com/watch?v=... or youtu.be/...)
    or just the 11-character video ID.
    
    Examples:
    
        yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ
        
        yttranscript dQw4w9WgXcQ --format markdown --timestamps
        
        yttranscript https://youtu.be/dQw4w9WgXcQ --output transcript.txt
        
        yttranscript dQw4w9WgXcQ --list-languages
    """
    try:
        # Validate URL and extract video info
        try:
            video = Video.from_url(url)
        except InvalidUrlError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("Expected format: https://youtube.com/watch?v=VIDEO_ID, https://youtu.be/VIDEO_ID, or VIDEO_ID", err=True)
            sys.exit(1)
        
        # Initialize extractor
        extractor = TranscriptExtractor()
        
        # Handle language listing
        if list_languages:
            if any([output_file, timestamps, output_format != 'plain']):
                click.echo("Error: --list-languages cannot be used with other output options", err=True)
                sys.exit(1)
            
            click.echo("Fetching available languages...")
            try:
                languages = extractor.list_available_languages(video.video_id)
                if not languages:
                    click.echo("No transcript languages available for this video.")
                    sys.exit(1)
                
                click.echo("Available languages:")
                for lang_info in languages:
                    status = " (auto-generated)" if lang_info.get('is_generated') else ""
                    click.echo(f"- {lang_info['language_code']} ({lang_info['language']}){status}")
                
            except (TranscriptNotAvailableError, NetworkError) as e:
                click.echo(f"Error: {e}", err=True)
                sys.exit(2)
            
            return
        
        # Extract transcript
        click.echo("Fetching transcript...")
        try:
            transcript = extractor.extract_transcript(video.video_id, language_code)
        except LanguageNotFoundError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(3)
        except (TranscriptNotAvailableError, NetworkError) as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(2)
        
        # Format transcript
        try:
            format_type = FormatType(output_format.lower())
            formatter = get_formatter(format_type)
            formatted_content = formatter.format(transcript, timestamps)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        
        # Output transcript
        if output_file:
            try:
                output_path = Path(output_file)
                
                # Check if file exists and handle overwrite
                if output_path.exists() and not force:
                    if not click.confirm(f"File '{output_file}' already exists. Overwrite?"):
                        click.echo("Operation cancelled.")
                        sys.exit(0)
                
                # Ensure parent directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write to file with UTF-8 encoding
                output_path.write_text(formatted_content, encoding='utf-8')
                click.echo(f"Transcript saved to '{output_file}'")
                
            except (OSError, IOError) as e:
                raise FileOutputError(f"Failed to write to '{output_file}': {e}")
        else:
            # Output to stdout
            click.echo(formatted_content)
    
    except FileOutputError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(5)
    except YttranscriptError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(99)
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(99)


if __name__ == '__main__':
    main()