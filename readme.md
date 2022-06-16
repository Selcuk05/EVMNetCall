## EVMNetCall
EVMNetCall is a desktop app for real time smart contract testing purposes.
As a dev or a user, you might not want to verify your contract on the explorer,
but still test it on the network without writing any code.
EVMNetCall comes in clutch, allowing you to call any external function repetitively by just entering
text inputs.

### Requirements
1. Contract ABI: You will need the ABI of your contract in a JSON file.
2. Ethereum Keystore: You will need an ethereum keystore.
    * You can create this using create_keystore.exe in the releases.

These requirements and the config must be in the same folder as the executable files.

### Configuration
```yaml
networks:
  eth-mainnet:
    name: "Ethereum Mainnet"
    rpc: "https://mainnet.infura.io/v3/"
  flare-sgb:
    name: "Flare Songbird Canary"
    rpc: "https://songbird.towolabs.com/rpc"
  flare-coston:
    name: "Flare Coston"
    rpc: "https://coston-api.flare.network/ext/bc/C/rpc"
```
You can add as many networks as you want using this configuration.
You will select one on the runtime.

### Contribution
Set up your virtual environment using `requirements.txt`<br/>
The usage of black & isort is highly recommended, but optional.<br/>
The software currently only works on Windows, if you port it onto Linux, make sure to open a pull request.