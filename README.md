# embed-pagination

## Notes
This project is a fork of an inactive repository at https://github.com/soosBot-com/Pagination<br>
Credit is due to the contributors of the original project.

## New features 💡
* Added new on_timeout options
* Added buttons for first/last page
* Improved button layout
* Many more general improvements


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the library.

```bash
pip install simple-embed-pagination
```

## Usage

> **Important:**
> discord.py master, or a form that has discord.ui.View is required to use this library!


### Quickstart
```python
import paginator

# Create a list of embeds to paginate.
embeds = [discord.Embed(title="First embed"),
          discord.Embed(title="Second embed"),
          discord.Embed(title="Third embed")]

... # Inside a command.
await paginator.Simple().start(ctx, pages=embeds)
```

> **Hint:**
> The `ctx` parameter is of type `discord.Interaction`

### Advanced

##### To use custom buttons, pass in the corresponding argument when you initiate the paginator. **THESE ARE OPTIONAL**

```python
# These arguments override the default ones.

PreviousButton = discord.ui.Button(...)
NextButton = discord.ui.Button(...)
PageCounterStyle = discord.ButtonStyle(...) # Only accepts discord.ButtonStyle
InitialPage = 0 # Page to start the paginator on.
OnTimeout = 'disable_view' # Delete paginator message on timeout. Default is False.
timeout = 400 # Seconds to timeout. Default is 60.
ephemeral = True # Defaults to False if not passed in.
FirstButton = discord.ui.Button(...)
LastButton = discord.ui.Button(...)

await paginator.Simple(
    previous_button=">",
    next_buttom=NextButton,
    page_counter_style=PageCounterStyle,
    initial_page=InitialPage,
    allow_ext_input=True,
    on_timeout=DeleteOnTimeout,
    timeout=timeout,
    ephemeral=ephemeral,
    first_button=FirstButton,
    last_button=LastButton
    
).start(ctx, pages=embeds)
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
