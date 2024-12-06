from django.forms.fields import ChoiceField


# Define the monkey patch
def patched_choice_field():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        from django_sorcery.fields import ModelChoiceField

        # Replace the problematic 'choices' property
        def _get_choices(self):
            return self._choices

        # Use the public 'choices' setter if available
        ModelChoiceField.choices = property(_get_choices, ChoiceField.choices.fset)

        print("Monkey patch applied to ModelChoiceField in django_sorcery.")

    except ImportError as e:
        print(f"Could not apply monkey patch: {e}")


patched_choice_field()
