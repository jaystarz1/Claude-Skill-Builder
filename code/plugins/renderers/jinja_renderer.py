"""
Minimal Jinja2-like template renderer (no external dependencies).
Supports basic variable substitution and simple loops.
"""
import re
from typing import Dict, Any


def render(template: str, context: Dict[str, Any]) -> str:
    """
    Render a template with the given context.
    Supports:
    - {{ variable }}
    - {% for item in items %}...{% endfor %}
    - {{ item.property }}
    """
    output = template
    
    # Handle for loops first
    output = _render_loops(output, context)
    
    # Handle variable substitution
    output = _render_variables(output, context)
    
    return output


def _render_variables(text: str, context: Dict[str, Any]) -> str:
    """Replace {{ variable }} with values from context."""
    def replace_var(match):
        var_name = match.group(1).strip()
        parts = var_name.split('.')
        
        value = context
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part, '')
            else:
                return ''
        
        return str(value) if value is not None else ''
    
    return re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_var, text)


def _render_loops(text: str, context: Dict[str, Any]) -> str:
    """Handle {% for item in items %}...{% endfor %}"""
    pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+(?:\.\w+)*)\s*-%?\}\s*(.*?)\s*\{%\s*endfor\s*%\}'
    
    def replace_loop(match):
        item_name = match.group(1)
        list_name = match.group(2)
        loop_body = match.group(3)
        
        # Get the list from context
        parts = list_name.split('.')
        items = context
        for part in parts:
            if isinstance(items, dict):
                items = items.get(part, [])
            else:
                items = []
        
        if not isinstance(items, list):
            return ''
        
        # Render each iteration
        result = []
        for i, item in enumerate(items):
            loop_context = context.copy()
            loop_context[item_name] = item
            loop_context['loop'] = {'index': i + 1, 'index0': i}
            
            iteration = loop_body
            # Replace loop variables
            iteration = re.sub(
                r'\{\{\s*' + item_name + r'(?:\.(\w+))?\s*\}\}',
                lambda m: str(item.get(m.group(1)) if m.group(1) and isinstance(item, dict) else item),
                iteration
            )
            iteration = re.sub(
                r'\{\{\s*loop\.(\w+)\s*\}\}',
                lambda m: str(loop_context['loop'].get(m.group(1), '')),
                iteration
            )
            result.append(iteration)
        
        return ''.join(result)
    
    return re.sub(pattern, replace_loop, text, flags=re.DOTALL)


def _render_conditionals(text: str, context: Dict[str, Any]) -> str:
    """Handle {% if condition %}...{% endif %} (basic support)."""
    pattern = r'\{%\s*if\s+(\w+(?:\.\w+)*)\s*%\}(.*?)\{%\s*endif\s*%\}'
    
    def replace_if(match):
        condition = match.group(1)
        content = match.group(2)
        
        # Get condition value
        parts = condition.split('.')
        value = context
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
        
        # Return content if truthy
        return content if value else ''
    
    return re.sub(pattern, replace_if, text, flags=re.DOTALL)
