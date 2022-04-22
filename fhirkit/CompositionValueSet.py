from fhirkit.ValueSet import VSCompose, ValueSet


class CompositionValueSet(ValueSet):
    compose: VSCompose

    def expand(self):
        for composition in self.compose.include:
            if len(composition.valueSet) > 0:
                pass
            if len(composition.concept) > 0:
                pass
            if len(composition.filter) > 0:
                pass
