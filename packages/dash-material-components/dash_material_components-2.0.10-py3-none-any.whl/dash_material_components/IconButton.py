# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class IconButton(Component):
    """An IconButton component.
IconButton component

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Component children.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- color (a value equal to: 'primary', 'secondary', 'error', 'inherit', 'success', 'info', 'warning'; optional):
    Button color.

- disableFocusRipple (boolean; optional):
    Disable focus ripple effect.

- disableRipple (boolean; optional):
    Disable ripple effect.

- disabled (boolean; optional):
    Disable button.

- edge (boolean | number | string | dict | list; optional):
    Use a negative margin to counteract the padding on one side.

- icon (string; optional):
    Icon name from
    https://mui.com/material-ui/material-icons/#search-material-icons.

- margin (number; optional):
    Box margin.

- nClicks (number; optional):
    Number of clicks.

- size (a value equal to: 'small', 'medium', 'large'; optional):
    Button size.

- sx (dict; optional):
    Disable elevation.

- width (string | number; optional):
    Box width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'IconButton'
    @_explicitize_args
    def __init__(self, children=None, icon=Component.UNDEFINED, color=Component.UNDEFINED, size=Component.UNDEFINED, margin=Component.UNDEFINED, width=Component.UNDEFINED, nClicks=Component.UNDEFINED, edge=Component.UNDEFINED, disabled=Component.UNDEFINED, disableRipple=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, sx=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'color', 'disableFocusRipple', 'disableRipple', 'disabled', 'edge', 'icon', 'margin', 'nClicks', 'size', 'sx', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'color', 'disableFocusRipple', 'disableRipple', 'disabled', 'edge', 'icon', 'margin', 'nClicks', 'size', 'sx', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(IconButton, self).__init__(children=children, **args)
