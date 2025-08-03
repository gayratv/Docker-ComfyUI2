#!/bin/bash
# Последний релиз ComfyUI

git ls-remote --tags https://github.com/comfyanonymous/ComfyUI.git \
    | grep -o 'refs/tags/[^{}]*$' \
    | sed 's#refs/tags/##' \
    | sort -V \
    | tail -n 1


git ls-remote --tags https://github.com/Comfy-Org/ComfyUI_frontend.git \
    | grep -o 'refs/tags/[^{}]*$' \
    | sed 's#refs/tags/##' \
    | sort -V \
    | tail -n 1