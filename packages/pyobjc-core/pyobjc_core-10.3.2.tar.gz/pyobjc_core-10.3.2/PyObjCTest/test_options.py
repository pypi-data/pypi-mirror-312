import objc
from PyObjCTools.TestSupport import TestCase


class TestOptions(TestCase):
    def test_verbose(self):
        orig = objc.options.verbose
        self.assertFalse(objc.options.verbose)
        try:
            objc.options.verbose = 1
            self.assertIs(objc.options.verbose, True)

            objc.options.verbose = ""
            self.assertIs(objc.options.verbose, False)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option 'verbose'"
            ):
                del objc.options.verbose

        finally:
            objc.options.verbose = orig

    def test_use_kvo(self):
        orig = objc.options.use_kvo
        self.assertTrue(objc.options.use_kvo)
        try:
            objc.options.use_kvo = 1
            self.assertIs(objc.options.use_kvo, True)

            objc.options.use_kvo = ""
            self.assertIs(objc.options.use_kvo, False)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option 'use_kvo'"
            ):
                del objc.options.use_kvo

        finally:
            objc.options.use_kvo = orig

    def test_unknown_pointer_raises(self):
        orig = objc.options.unknown_pointer_raises
        self.assertFalse(objc.options.unknown_pointer_raises)
        try:
            objc.options.unknown_pointer_raises = 1
            self.assertIs(objc.options.unknown_pointer_raises, True)

            objc.options.unknown_pointer_raises = ""
            self.assertIs(objc.options.unknown_pointer_raises, False)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option 'unknown_pointer_raises'"
            ):
                del objc.options.unknown_pointer_raises

        finally:
            objc.options.unknown_pointer_raises = orig

    def test_structs_indexable(self):
        orig = objc.options.structs_indexable
        self.assertTrue(objc.options.structs_indexable)
        try:
            objc.options.structs_indexable = 1
            self.assertIs(objc.options.structs_indexable, True)

            objc.options.structs_indexable = ""
            self.assertIs(objc.options.structs_indexable, False)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option 'structs_indexable'"
            ):
                del objc.options.structs_indexable

        finally:
            objc.options.structs_indexable = orig

    def test_structs_writable(self):
        orig = objc.options.structs_writable
        self.assertTrue(objc.options.structs_writable)
        try:
            objc.options.structs_writable = 1
            self.assertIs(objc.options.structs_writable, True)

            objc.options.structs_writable = ""
            self.assertIs(objc.options.structs_writable, False)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option 'structs_writable'"
            ):
                del objc.options.structs_writable

        finally:
            objc.options.structs_writable = orig

    def test_nscodiing_version(self):
        orig = objc.options._nscoding_version
        try:
            objc.options._nscoding_version = 2
            self.assertEqual(objc.options._nscoding_version, 2)

            with self.assertRaisesRegex(
                TypeError,
                r"('str' object cannot be interpreted as an integer)|(an integer is required \(got type str\))",
            ):
                objc.options._nscoding_version = ""

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_nscoding_version'"
            ):
                del objc.options._nscoding_version

        finally:
            objc.options._nscoding_version = orig

    def test_mapping_count(self):
        orig = objc.options._mapping_count
        try:
            objc.options._mapping_count = 2
            self.assertEqual(objc.options._mapping_count, 2)

            with self.assertRaisesRegex(
                TypeError, "'str' object cannot be interpreted as an integer"
            ):
                objc.options._mapping_count = ""

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_mapping_count'"
            ):
                del objc.options._mapping_count

        finally:
            objc.options._mapping_count = orig

    def test_deprecation_warnings(self):
        orig = objc.options.deprecation_warnings
        self.assertEqual(objc.options.deprecation_warnings, "0.0")
        try:
            objc.options.deprecation_warnings = "10.2"
            self.assertEqual(objc.options.deprecation_warnings, "10.2")

            with self.assertRaisesRegex(
                TypeError,
                r"Expecting 'str' value for 'objc.options.deprecation_warnings', got instance of 'float'",
            ):
                objc.options.deprecation_warnings = 43.5

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option 'deprecation_warnings'"
            ):
                del objc.options.deprecation_warnings

        finally:
            objc.options.deprecation_warnings = orig

    def test_nscoding_encoder(self):
        orig = objc.options._nscoding_encoder
        value = object()
        try:
            objc.options._nscoding_encoder = value
            self.assertIs(objc.options._nscoding_encoder, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_nscoding_encoder'"
            ):
                del objc.options._nscoding_encoder

        finally:
            objc.options._nscoding_encoder = orig

    def test_nscoding_decoder(self):
        orig = objc.options._nscoding_decoder
        value = object()
        try:
            objc.options._nscoding_decoder = value
            self.assertIs(objc.options._nscoding_decoder, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_nscoding_decoder'"
            ):
                del objc.options._nscoding_decoder

        finally:
            objc.options._nscoding_decoder = orig

    def test_copy(self):
        orig = objc.options._copy
        value = object()
        try:
            objc.options._copy = value
            self.assertIs(objc.options._copy, value)

            with self.assertRaisesRegex(AttributeError, "Cannot delete option '_copy'"):
                del objc.options._copy

        finally:
            objc.options._copy = orig

    def test_class_extender(self):
        orig = objc.options._class_extender
        value = object()
        try:
            objc.options._class_extender = value
            self.assertIs(objc.options._class_extender, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_class_extender'"
            ):
                del objc.options._class_extender

        finally:
            objc.options._class_extender = orig

    def test_make_bundleForClass(self):
        orig = objc.options._make_bundleForClass
        value = object()
        try:
            objc.options._make_bundleForClass = value
            self.assertIs(objc.options._make_bundleForClass, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_make_bundleForClass'"
            ):
                del objc.options._make_bundleForClass

        finally:
            objc.options._make_bundleForClass = orig

    def test_nsnumber_wrapper(self):
        orig = objc.options._nsnumber_wrapper
        value = object()
        try:
            objc.options._nsnumber_wrapper = value
            self.assertIs(objc.options._nsnumber_wrapper, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_nsnumber_wrapper'"
            ):
                del objc.options._nsnumber_wrapper

        finally:
            objc.options._nsnumber_wrapper = orig

    def test_callable_doc(self):
        orig = objc.options._callable_doc
        value = object()
        try:
            objc.options._callable_doc = value
            self.assertIs(objc.options._callable_doc, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_callable_doc'"
            ):
                del objc.options._callable_doc

        finally:
            objc.options._callable_doc = orig

    def test_callable_signature(self):
        orig = objc.options._callable_signature
        value = object()
        try:
            objc.options._callable_signature = value
            self.assertIs(objc.options._callable_signature, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_callable_signature'"
            ):
                del objc.options._callable_signature

        finally:
            objc.options._callable_signature = orig

    def test_mapping_types(self):
        orig = objc.options._mapping_types
        value = object()
        try:
            objc.options._mapping_types = value
            self.assertIs(objc.options._mapping_types, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_mapping_types'"
            ):
                del objc.options._mapping_types

        finally:
            objc.options._mapping_types = orig

    def test_sequence_types(self):
        orig = objc.options._sequence_types
        value = object()
        try:
            objc.options._sequence_types = value
            self.assertIs(objc.options._sequence_types, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_sequence_types'"
            ):
                del objc.options._sequence_types

        finally:
            objc.options._sequence_types = orig

    def test_set_types(self):
        orig = objc.options._set_types
        value = object()
        try:
            objc.options._set_types = value
            self.assertIs(objc.options._set_types, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_set_types'"
            ):
                del objc.options._set_types

        finally:
            objc.options._set_types = orig

    def test_date_types(self):
        orig = objc.options._date_types
        value = object()
        try:
            objc.options._date_types = value
            self.assertIs(objc.options._date_types, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_date_types'"
            ):
                del objc.options._date_types

        finally:
            objc.options._date_types = orig

    def test_datetime_date_type(self):
        orig = objc.options._datetime_date_type
        value = object()
        try:
            objc.options._datetime_date_type = value
            self.assertIs(objc.options._datetime_date_type, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_datetime_date_type'"
            ):
                del objc.options._datetime_date_type

        finally:
            objc.options._datetime_date_type = orig

    def test_datetime_datetime_type(self):
        orig = objc.options._datetime_datetime_type
        value = object()
        try:
            objc.options._datetime_datetime_type = value
            self.assertIs(objc.options._datetime_datetime_type, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_datetime_datetime_type'"
            ):
                del objc.options._datetime_datetime_type

        finally:
            objc.options._datetime_datetime_type = orig

    def test_getKey(self):
        orig = objc.options._getKey
        value = object()
        try:
            objc.options._getKey = value
            self.assertIs(objc.options._getKey, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_getKey'"
            ):
                del objc.options._getKey

        finally:
            objc.options._getKey = orig

    def test_setKey(self):
        orig = objc.options._setKey
        value = object()
        try:
            objc.options._setKey = value
            self.assertIs(objc.options._setKey, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_setKey'"
            ):
                del objc.options._setKey

        finally:
            objc.options._setKey = orig

    def test_getKeyPath(self):
        orig = objc.options._getKeyPath
        value = object()
        try:
            objc.options._getKeyPath = value
            self.assertIs(objc.options._getKeyPath, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_getKeyPath'"
            ):
                del objc.options._getKeyPath

        finally:
            objc.options._getKeyPath = orig

    def test_setKeyPath(self):
        orig = objc.options._setKeyPath
        value = object()
        try:
            objc.options._setKeyPath = value
            self.assertIs(objc.options._setKeyPath, value)

            with self.assertRaisesRegex(
                AttributeError, "Cannot delete option '_setKeyPath'"
            ):
                del objc.options._setKeyPath

        finally:
            objc.options._setKeyPath = orig

    def test_bundle_hack_used(self):
        self.assertFalse(objc.options._bundle_hack_used)

        with self.assertRaisesRegex(
            AttributeError,
            "attribute '_bundle_hack_used' of 'objc._OptionsType' objects is not writable",
        ):
            objc.options._bundle_hack_used = 1

        with self.assertRaisesRegex(
            AttributeError,
            "attribute '_bundle_hack_used' of 'objc._OptionsType' objects is not writable",
        ):
            del objc.options._bundle_hack_used
