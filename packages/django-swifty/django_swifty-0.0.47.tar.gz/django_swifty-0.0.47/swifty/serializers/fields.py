"""Constants"""

from typing import Dict, Tuple, Any
from datetime import date
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from swifty.expressionator.manager import ExpressionatorManager
from swifty.utils.helpers import validation_error_detail


class BasicFieldSerializer:
    """
    _summary_

    Args:
        object (_type_): _description_
    """

    static_args = (
        "read_only",
        "write_only",
        "required",
        "default",
        "initial",
        "source",
        "label",
        "help_text",
        "style",
        "error_messages",
        "validators",
        "allow_null",
    )
    extra_args: Tuple[str, ...] = tuple()
    empty_value: Any = None
    data = None
    default_empty_html = None

    def __init__(self, *args, extra_kwargs=None, parent=None, **kwargs):
        self.extra_kwargs = extra_kwargs or {}
        self.parent = parent
        super(BasicFieldSerializer, self).__init__(*args, **kwargs)

    @property
    def expressionator(self) -> ExpressionatorManager:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        return getattr(self.parent, "expressionator", ExpressionatorManager)(
            data=getattr(self.parent, "initial_data", {})
        )

    def initialator(self):
        """_summary_

        Args:
            data (_type_): _description_
        """
        initialator = self.extra_kwargs.get("initialator")
        if initialator:
            initial_attrs = (
                self.expressionator.initialator(initialization_data=initialator) or {}
            )
            for attr, value in initial_attrs.items():
                self.extra_kwargs[attr] = value

    def to_internal_value(self, data):
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.initialator()
        return super(BasicFieldSerializer, self).to_internal_value(data)

    def to_representation(self, data):
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.initialator()
        return super(BasicFieldSerializer, self).to_representation(data)

    def is_disabled_by_rules(self, enabled_rules):
        """_summary_

        Args:
            enabled_rules (_type_): _description_

        Returns:
            _type_: _description_
        """
        is_disabled = self.extra_kwargs.get("disabled") or False
        if not is_disabled and isinstance(enabled_rules, (list, tuple)):
            for rule in enabled_rules:
                valid_values = rule.get("value")
                field_value = self.expressionator.get_value(rule.get("field_name"))
                if not field_value or valid_values and field_value not in valid_values:
                    return True
        return is_disabled

    def trigger_validator(self, validator, value):
        """_summary_

        Args:
            validator (_type_): _description_
            value (_type_): _description_

        Raises:
            ValidationError: _description_
        """
        default_message = validator.get("default")
        result = self.expressionator.validator(validation_data=validator, value=value)
        if not result:
            raise ValidationError(detail=default_message)

    def run_validation(self, value=empty):
        """_summary_

        Args:
            value (_type_, optional): _description_. Defaults to empty.

        Returns:
            _type_: _description_
        """
        if (
            self.is_disabled_by_rules(
                enabled_rules=self.extra_kwargs.get("enabled_rules")
            )
            or not self.required
        ) and not value:
            return value
        if (validator := self.extra_kwargs.get("validator")) and not (
            self.parent.is_update
            and self.extra_kwargs.get("field_name") != self.parent.pk_field
        ):
            self.trigger_validator(
                validator=validator,
                value=value,
            )
        return super().run_validation(value)


class CharField(BasicFieldSerializer, serializers.CharField):
    """
    A serializer field for handling character (string) data.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
    )
    empty_value: Any = ""


class EmailField(BasicFieldSerializer, serializers.EmailField):
    """
    A serializer field for handling email addresses.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
    )
    empty_value: Any = ""


class URLField(BasicFieldSerializer, serializers.URLField):
    """
    A serializer field for handling URLs.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
    )
    empty_value: Any = ""


class UUIDField(BasicFieldSerializer, serializers.UUIDField):
    """
    A serializer field for handling UUIDs.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
        "format",
        "hex_verbose",
    )
    empty_value: Any = ""


class IntegerField(BasicFieldSerializer, serializers.IntegerField):
    """
    A serializer field for handling integers.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("max_value", "min_value")
    empty_value: Any = 0


class FloatField(BasicFieldSerializer, serializers.FloatField):
    """
    A serializer field for handling floats.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("max_value", "min_value")
    empty_value: Any = 0.0


class DecimalField(BasicFieldSerializer, serializers.DecimalField):
    """
    A serializer field for handling decimals.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "max_digits",
        "decimal_places",
        "coerce_to_string",
        "max_value",
        "min_value",
        "normalize_output",
        "localize",
        "rounding",
    )
    empty_value: Any = 0.0


class BooleanField(BasicFieldSerializer, serializers.BooleanField):
    """
    A serializer field for handling booleans.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("allow_null",)
    empty_value: Any = False


class DateField(BasicFieldSerializer, serializers.DateField):
    """
    A serializer field for handling dates.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("format", "input_formats")

    def __init__(self, *args, **kwargs):
        input_formats = ["iso-8601", "%Y-%m-%dT%H:%M:%S.%fZ"]
        self.initial = self.initial if self.initial is not None else date.today()
        super().__init__(*args, input_formats=input_formats, **kwargs)


class DateTimeField(BasicFieldSerializer, serializers.DateTimeField):
    """
    A serializer field for handling date-times.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("format", "input_formats", "default_timezone")


class TimeField(BasicFieldSerializer, serializers.TimeField):
    """
    A serializer field for handling time values.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("format", "input_formats")


class DurationField(BasicFieldSerializer, serializers.DurationField):
    """
    A serializer field for handling duration values.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args = ("max_value", "min_value")


class ListField(BasicFieldSerializer, serializers.ListField):
    """
    A serializer field for handling lists.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("child", "allow_empty", "max_length", "min_length")
    empty_value: Any = []


class DictField(BasicFieldSerializer, serializers.DictField):
    """
    A serializer field for handling dictionaries.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("child", "allow_empty")
    empty_value: Any = {}


class ChoiceField(BasicFieldSerializer, serializers.ChoiceField):
    """
    A serializer field for handling choices.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "choices",
        "html_cutoff",
        "html_cutoff_text",
        "allow_blank",
    )

    def __init__(self, choices=None, **kwargs):
        choices = choices or ()
        super().__init__(choices=choices, **kwargs)


class MultipleChoiceField(BasicFieldSerializer, serializers.MultipleChoiceField):
    """
    A serializer field for handling ultiple choices.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args = (
        "choices",
        "html_cutoff",
        "html_cutoff_text",
        "allow_blank",
        "allow_empty",
    )
    empty_value = []

    def __init__(self, choices=None, **kwargs):
        choices = choices or ()
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return list(super().to_internal_value(data))


class SlugField(BasicFieldSerializer, serializers.SlugField):
    """
    A serializer field for handling slugs.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("allow_unicode",)
    empty_value: Any = ""


class FileField(BasicFieldSerializer, serializers.FileField):
    """
    A serializer field for handling file uploads.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("allow_empty_file", "use_url", "max_length")


class ImageField(BasicFieldSerializer, serializers.ImageField):
    """
    A serializer field for handling image uploads.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_empty_file",
        "use_url",
        "max_length",
        "_DjangoImageField",
    )


class SerializerMethodField(BasicFieldSerializer, serializers.SerializerMethodField):
    """
    A serializer field for handling method-based fields.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("method_name", "source", "read_only")

    def to_internal_value(self, data):
        return data


class HyperlinkedIdentityField(
    BasicFieldSerializer, serializers.HyperlinkedIdentityField
):
    """
    A serializer field for handling hyperlinked identity.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "view_name",
        "lookup_field",
        "lookup_url_kwarg",
        "format",
        "read_only",
        "source",
    )


class HyperlinkedRelatedField(
    BasicFieldSerializer, serializers.HyperlinkedRelatedField
):
    """
    A serializer field for handling hyperlinked relations.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "view_name",
        "lookup_field",
        "lookup_url_kwarg",
        "format",
    )


class PrimaryKeyRelatedField(BasicFieldSerializer, serializers.PrimaryKeyRelatedField):
    """
    A serializer field for handling primary key relations.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "pk_field",
        "queryset",
        "many",
        "read_only",
        "html_cutoff",
        "html_cutoff_text",
    )


class RelatedField(BasicFieldSerializer, serializers.RelatedField):
    """
    A serializer field for handling related objects.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "queryset",
        "many",
        "read_only",
        "html_cutoff",
        "html_cutoff_text",
    )

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class JSONField(BasicFieldSerializer, serializers.JSONField):
    """
    A serializer field for handling JSON objects.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("binary", "encoder", "decoder")
    empty_value: Any = {}


class ReadOnlyField(BasicFieldSerializer, serializers.ReadOnlyField):
    """
    A serializer field for read-only data.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    def to_internal_value(self, data):
        return data


class HiddenField(BasicFieldSerializer, serializers.HiddenField):
    """
    A serializer field for hidden data.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    def to_representation(self, value):
        return value


class SectionFieldException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, *args, field_path=None, error=None, **kwargs) -> None:
        self.field_path = field_path
        self.error = error
        super().__init__(*args, **kwargs)


class BaseSectionField(serializers.JSONField):
    """
    _summary_

    Args:
        JSONField (_type_): _description_
    """

    extra_args = ("binary", "encoder", "decoder", "section")
    extra_kwargs = None

    def __init__(self, **filtered_kwargs):
        """
        _summary_

        Args:
            section (_type_, optional): _description_. Defaults to None.
        """
        from swifty.serializers.manager import create_field_kwargs

        self.section = self.extra_kwargs and self.extra_kwargs.get("section", {})
        self.fields = {}
        for field_props in self.section.get("fields", []):
            field_base, field_kwargs = create_field_kwargs(field_props)
            self.fields[field_props["field_name"]] = field_base(
                parent=self, **field_kwargs
            )

        super().__init__(**filtered_kwargs)

    def to_internal_value(self, data):
        # Recursively validate nested fields
        errors = {}
        if isinstance(data, dict):
            for key, value in data.items():
                try:
                    data[key] = self.fields[key].run_validation(value)
                except (ValidationError, DjangoValidationError) as error:
                    errors.update(
                        {key: ValidationError(detail=validation_error_detail(error))}
                    )
                except KeyError:
                    pass

        if errors:
            raise ValidationError(detail=validation_error_detail(errors))
        return super().to_internal_value(data)


class SectionField(BasicFieldSerializer, BaseSectionField):
    """
    _summary_

    Args:
        JSONField (_type_): _description_
    """

    empty_value = {}


class SectionManyField(BasicFieldSerializer, BaseSectionField):
    """
    _summary_

    Args:
        JSONField (_type_): _description_
    """

    empty_value = []

    def to_internal_value(self, data_list):
        # Recursively validate nested fields
        cleaned_data = []
        errors = {}
        for data in data_list:
            if isinstance(data, dict):
                try:
                    cleaned_data.append(super().to_internal_value(data))
                except (ValidationError, DjangoValidationError) as error:
                    errors.update(
                        {
                            data_list.index(data): ValidationError(
                                detail=validation_error_detail(error)
                            )
                        }
                    )

        if errors:
            raise ValidationError(detail=validation_error_detail(errors))
        return cleaned_data


FIELD_TYPE_MAP: Dict[str, BasicFieldSerializer] = {
    field_serializer.__name__: field_serializer
    for field_serializer in BasicFieldSerializer.__subclasses__()
}
