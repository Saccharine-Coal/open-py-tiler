from core.math.transformations import scalers, projections, translations

p = (1, 1, 1)

a = scalers.ScalingMatrix3(1)
a.scale(5)
b = projections.IsometricProjection(1)
c = translations.TranslationMatrix3((1, 1, 1))
print(b.transform(c.transform(a.transform(p))))
