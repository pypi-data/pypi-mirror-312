from typing import Optional, cast

from pycoingecko.utils import CoinGeckoApiUrls, CoinGeckoRequestParams, IHttp


class NFTs:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def nft_list(
        self,
        *,
        order: Optional[str] = None,
        per_page: Optional[int] = 100,
        page: Optional[int] = 1,
    ) -> list:
        """Query all supported NFTs with id, contract address, name, asset platform id and symbol on CoinGecko.

        :param order:     Sort results by field
        :param per_page:  Total results per page
        :param page:      Page through results
        """
        params = {}
        request: CoinGeckoRequestParams = {}

        if order:
            params["order"] = order

        if per_page:
            params["per_page"] = per_page  # type: ignore

        if page:
            params["page"] = page  # type: ignore

        if params:
            request = {"params": params}

        response = self.http.send(path=CoinGeckoApiUrls.NFTS, **request)

        return cast(list, response)

    def collection_by_id(self, *, collection_id: str) -> dict:
        """Query all the NFT data (name, floor price, 24 hr volume....) based on the nft collection id.

        :param collection_id:     The NFT collection id
        """
        path = CoinGeckoApiUrls.NFTS_COLLECTION.format(id=collection_id)
        response = self.http.send(path=path)

        return cast(dict, response)

    def collection_by_contract_address(
        self, *, asset_platform_id: str, contract_address: str
    ) -> dict:
        """Query all the NFT data (name, floor price, 24 hr volume....) based on the nft collection contract address and respective asset platform.

        :param asset_platform_id:     The asset platform id
        :param contract_address:      The contract address of a token
        """
        path = CoinGeckoApiUrls.NFTS_COLLECTION_CONTRACT_ADDRESS.format(
            asset_platform_id=asset_platform_id, contract_address=contract_address
        )
        response = self.http.send(path=path)

        return cast(dict, response)
