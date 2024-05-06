# DRF Pagination Meta Wrap
Wrap your DRF pagination meta data

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
    - [Providing Additional Meta](#providing-additional-meta)
- [How it works](#how-it-works)
- [Customizing](#customizing)
  - [Custom Meta Key](#custom-meta-key)
  - [Custom Data Key](#custom-data-key)
- [OpenApi Schema Generation](#openapi-schema-generation)
  - [Additional Metadata Schema](#additional-metadata-schema)
- [Contributing](#contributing)


## Installation
1. Install the package using pip:

```bash
pip install drf-pagination-meta-wrap
```

2. Add `drf_pagination_meta_wrap` to `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    ...,
    "drf_pagination_meta_wrap",
]
```


## Usage
Extend the `Pagination` class with `WrapPaginationMetadataMixin` class provideed by the package.

Lets take an example with BlogPagination class.
```python
class BlogPagination(WrapPaginationMetadataMixin, PageNumberPagination):
    pass
```

Now the response will look like:
```json
{
    "meta": {
        "count": 10,
        "next": "http://127.0.0.1:8000/api/blogs/?page=2",
        "previous": null
    },
    "results": [...]
}
```

This works for all pagination classes.

### Providing Additional Meta
If you want to add additional meta data to the `meta` key of the response, you can set the `additional_metadata` in the `WrapPaginationMetadataMixin` class.

```python
class BlogPagination(WrapPaginationMetadataMixin, PageNumberPagination):
    additional_metadata = {
        "foo": "bar",
    }
```

Or you can use the `get_additional_metadata` method.

```python
class BlogPagination(WrapPaginationMetadataMixin, PageNumberPagination):
    def get_additional_metadata(self):
        return {
            "foo": "bar",
        }
```
Now the pagination response will have another `foo` key in the `meta`.

**Note:** *if you need to generate the OpenApi Schema for the additional metadata, read [additional metadata schema](#additional-metadata-schema)*

## How it works
The `WrapPaginationMetadataMixin` mixin wraps everything in `meta` key except `results`.

## Customizing
### Custom Meta Key
You can customize the `meta` key. By default it is `meta`. You can customize it by setting the `paginated_response_meta_key` in the class.

```python
class BlogPagination(WrapPaginationMetadataMixin, PageNumberPagination):
    paginated_response_meta_key = "metadata"
```

Or if you want it globally, you can set the `PAGINATED_RESPONSE_META_KEY` in the package settings.

```python
DRF_PAGINATION_META_WRAP = {
    "PAGINATED_RESPONSE_META_KEY" = "metadata"
}
```

### Custom Data Key
You can customize the `data` key. By default it is `results`. You can customize it by setting the `paginated_response_data_key` in the class.

```python
class BlogPagination(WrapPaginationMetadataMixin, PageNumberPagination):
    paginated_response_data_key = "data"
```

Or if you want it globally, you can set the `PAGINATED_RESPONSE_DATA_KEY` in the package settings.

```python
DRF_PAGINATION_META_WRAP = {
    "PAGINATED_RESPONSE_DATA_KEY" = "data"
}
```

## OpenApi Schema Generation
The `WrapPaginationMetadataMixin` mixin generates the OpenApi schema for the pagination response.

### Additional Metadata Schema
If you have [additional metadata](#providing-additional-meta), the mixin will try to auto generate its schema by introspecting the `get_additional_metadata` method. This may not work properly for all cases.

For example if your Pagination class is used in a authenticated request context, it will fail.

In this case, you have to manually provide the `additional_metadata` properties in `get_additional_metadata_properties_schema` method.

```python
class BlogPagination(WrapPaginationMetadataMixin, PageNumberPagination):
    additional_metadata = {
        "foo": "bar",
    }

    def get_additional_metadata_properties_schema(self):
        return {
            "foo": {
                "type": "string",
                "example": "bar",
            },
        }
```

### Contributing
Contributions are more than welcome! Please open an issue if you have any questions or suggestions.