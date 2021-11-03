SMH_ROOT_SEARCH_URL = 'https://api.smh.com.au/graphql'

SMH_ROOT_ARTICLE_CONTENT_URL = 'https://api.smh.com.au/api/content/v0/assets/'

SMH_BASE_SEARCH_VARIABLES = {"brand":"smh","offset":0,"pageSize":20}

SMH_SEARCH_QUERY = """
query SearchResultQuery($query: String!, $brand: String!, $offset: Int!, $pageSize: Int! ) 
{
    assetsConnection: publicSearch(query: $query, brand: $brand, offset: $offset, pageSize: $pageSize) { 
        ...AssetsConnectionFragment_showMoreOffsetData 
    } 
}

fragment AssetsConnectionFragment_showMoreOffsetData on AssetsConnection { 
    assets { 
        ...AssetFragmentFragment_assetDataWithTag
        id 
    }
    pageInfo { 
        endOffset hasNextPage 
    } 
    totalCount
} 

fragment AssetFragmentFragment_assetDataWithTag on Asset {
    ...AssetFragmentFragment_assetData 
    tags {
        primaryTag { 
            ...AssetFragment_tagFragment 
        } 
    }
} 

fragment AssetFragmentFragment_assetData on Asset { 
    id 
    asset {
        about 
        byline
        duration
        headlines {
            headline
        } 
        live 
        totalImages 
    } 

    label 
    urls {
        canonical { 
            path 
            brand 
        } 
        external
    } 
    assetType 
    dates { 
        modified
        published 
    } 
    sponsor { 
        name 
    } 
} 

fragment AssetFragment_tagFragment on AssetTagDetails { 
    displayName 
} 
"""