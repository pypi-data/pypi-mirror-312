# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2024-12-01

### Changed

* Add overloaded signatures to `parse_file_content` and `parse_string` to provide accurate
return types based on the length of `separators` tuple passed as an argument

## [2.0.0] - 2024-06-19

### Added

* `dict_to_object` function to convert a dictionary to an object
* `CaptureMalloc` context manager class to capture memory allocations within a block of code
* `parse_string` function to parse a string using the provided arguments
It's identical to the `parse_file_content` function but works with strings instead of files

### Changed

* `parse_file_content` function now accepts a tuple of separators as an argument, 
instead of having a separate argument for each separator. Additionally, the function now
has no limit on the number of separators that can be provided. However, type hints for the
function support only up to 5 separators, since recursive type hints are not widely supported,
and it's unlikely that more than 5 separators will be needed.

### Removed

* `read_file` decorator has been removed in favor of the more versatile `parse_file_content` function
* `memoize` decorator has been removed due to redundancy - `functools.lru_cache` can be used instead,
with no loss of functionality or performance

## [1.1.0] - 2024-04-22

### Added

* Introduce the `parse_file_content` function as an alternative to the `read_file` decorator -
  the `parse_file_content` function provides equivalent functionality to the `read_file` decorator but in a
  more versatile and widely applicable form

### Deprecated

* Deprecate the `read_file` decorator in favor of the `parse_file_content` function.
  The `read_file` decorator is no longer recommended for use and will be removed in a future release.
  Users are encouraged to migrate to the `parse_file_content` function for file parsing functionality.

## [1.0.2] - 2024-03-27

### Changed

* Fix the issue, where the `stopwatch` decorator, when used on recursive functions,
  would start a new timer for each recursive call - now, the decorator will only
  start a timer for the first call and return the total time taken by the function
  and all its recursive calls

## [1.0.1] - 2024-03-04

### Changed

* Update project links in `pyproject.toml`

## [1.0.0] - 2024-03-03

### Added

* Official release of the package
