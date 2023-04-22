The `mappings` property contains a dictionary where:

`key`: a string with the deck that the tags should be mapped to

`value`: an array of string, each being a tag that should be added to the deck

An example:

```
{
    "mappings": {
        "Family": ["John", "Maria"]
    }
}
```

Notes with the tag "John" or "Maria" will be added to the deck "Family" automatically.

The `ignoredTags` property contains an array of strings. Each element is a tag for which the adding behavior will be as
it is without this plugin.