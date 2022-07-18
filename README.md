# fbi/open-up

**tl;dr** "Debug" finicky CI failures

Have you ever encountered a finicky CI problem where you feel like yelling "I JUST WANT A TERMINAL WITH THE AGENT" at the screen? Well, this little hacky pile of garbage will allow you to bust into your agent jobs and _actually do that_. 

The project is quite simple, but should meet MOST of your debugging needs. It uses an Azure Storage Queue on an account YOU control to pass messages back and forth from the agent to a place where your local CLI can grab them.

- On a windows agent, commands are invoked via `pwsh`.
- On mac/linux, commands will be invoked via `bash`.

## Example Usage

`.github/workflows/<your-problem-action>.yml`
```yml
- bash: |
    pip install fbi-open-up
    fbi -c "<connection string>"
  displayName: "A step inserted into your problem build"
# you can optionally skip the arguments above and used the connection strings defined below 
```

_On your machine._
```bash
/>openup "<connection string>"
```

_In a github action._
```yml
steps:
  # <your normal job steps having issues here>
  # fbi-open-up takes a dep on python > 3. it does not update your selected python version though
  - uses: semick-dev/fbi-open-up
    with:
      fbi-queue-cs:
      fbi-queue-name: 'agent-actions' # this is not required, but will default to `agent-interactions
      fbi-max-iterations: '180' # time in seconds this thing will be waiting for
```

## Command Details

Install

```bash
pip install fbi-open-up
```

`fbi -h`

```text
usage: fbi [-h] [-c CS] [-v--verbose]

This CLI app is used on a devops or actions agent to respond to debugging messages.

optional arguments:
  -h, --help            show this help message and exit
  -c CS, --connectionstring CS
                        The blob storage connection string. If not provided, will fall back to FBI_CONNECTION_STRING.
  -v--verbose           Verbosity setting.
```

`openup -h`

```text
usage: openup [-h] [-c CS] [-v--verbose]

This CLI app is used on a user's machine, and is used to interact with the remote devops agent.

optional arguments:
  -h, --help            show this help message and exit
  -c CS, --connectionstring CS
                        The blob storage connection string. If not provided, will fall back to FBI_CONNECTION_STRING.
  -v--verbose           Verbosity setting.
```

## Environment Variables

Both `fbi` and `openup` honor the following variables.

| Variable Name        | Description                                                                                                                                |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `FBI_QUEUE_CS`       | Connection string used to communicate with the azure-storage-account. If provided via command line argument, this value will be ignored.   |
| `FBI_QUEUE_NAME`     | The prefix of the queues used for this session. `agent-interactions` becomes `agent-interactions-control` and `agent-interactions-output`. |
| `FBI_MAX_ITERATIONS` | The number of `sleep` cycles the app will run before exiting. Defaults to 3 minutes to save on CI time.                                    |

## Important gotcha about running the agent

If you're using a standard Azure Storage Account on your personal account, you will need to update the firewall rules such that your CI agent can actually communicate with the storage account.

If you don't do this, you may get weird `403` errors with "not authorized to do that" even with a correctly set connection string.
