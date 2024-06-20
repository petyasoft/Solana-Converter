from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, Bip44Changes, base58


class BlockChainAccount():
    def __init__(self, mnemonic, coin_type=Bip44Coins.SOLANA, password = '') -> None:
        self.mnemonic = mnemonic.strip()
        self.coin_type = coin_type
        self.password = password 

    def get_address(self,count):
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate(self.password)
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT) # if you use "Solflare", remove this line and make a simple code modify and test
        priv_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()
        public_key_bytes = bip44_chg_ctx.PublicKey().RawCompressed().ToBytes()[1:]
        key_pair = priv_key_bytes+public_key_bytes
        return {"mnemonic" : self.mnemonic,
                "address" : bip44_chg_ctx.PublicKey().ToAddress(),
                "private" : base58.Base58Encoder.Encode(key_pair)}

    
with open("address.txt",'w') as file:
    pass
with open("private.txt",'w') as file:
    pass
with open("alldata.txt",'w') as file:
    pass

with open("mnemonics.txt",'r') as file:
    mnemonics = [mnemo.strip() for mnemo in file.readlines()]
for mnemonic in mnemonics:
    COUNT_DERIVATION_PATH = 1
    for count in range(COUNT_DERIVATION_PATH):
        try:
            keys = BlockChainAccount(mnemonic=mnemonic)
            info = keys.get_address(count)
            with open("address.txt",'a') as file:
                file.write(info["address"]+'\n')
            with open("private.txt",'a') as file:
                file.write(info["private"]+'\n')
            with open("alldata.txt",'a') as file:
                file.write(info["mnemonic"]+' '+info["private"]+' '+info["address"]+'\n')
        except:
            continue
