from typing import Dict, Any

def heal_code(code: str, error_message: str, error_type: str) -> Dict[str, Any]:
    lines = code.split('\n')
    patches_applied = []
    confidence = 0.0
    
    if error_type == 'NameError':
        if "is not defined" in error_message:
            var_name = error_message.split("'")[1]
            lines.insert(0, f"{var_name} = None  # Auto-healed: added missing variable definition")
            patches_applied.append({'type': 'NameError', 'line': 1, 'description': f'Added missing variable {var_name}'})
            confidence = 0.8
            
    elif error_type in ('ImportError', 'ModuleNotFoundError'):
        if "No module named" in error_message:
            mod_name = error_message.split("'")[1]
            lines.insert(0, f"import {mod_name}  # Auto-healed: added missing import")
            patches_applied.append({'type': 'ImportError', 'line': 1, 'description': f'Added import {mod_name}'})
            confidence = 0.9
            
    elif error_type == 'TypeError':
        if "can only concatenate str (not \"int\") to str" in error_message:
            patches_applied.append({'type': 'TypeError', 'line': 0, 'description': 'Requires manual string casting'})
            confidence = 0.2
            
    elif error_type == 'AttributeError':
        if "'NoneType' object has no attribute" in error_message:
            attr = error_message.split("'")[-2]
            patches_applied.append({'type': 'AttributeError', 'line': 0, 'description': f'Null check needed for {attr}'})
            confidence = 0.5
            
    patched_code = '\n'.join(lines)
    return {
        'patched_code': patched_code,
        'patches_applied': patches_applied,
        'confidence': confidence
    }
