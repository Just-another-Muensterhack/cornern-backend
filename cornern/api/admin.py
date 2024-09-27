from django.contrib import admin

from .models import Corner, Feedback, Measurement, Sensor

admin.site.site_header = "Cornern Admin"
admin.site.index_title = "Cornern Admin"
admin.site.site_title = "Cornern Admin"


class SensorInline(admin.TabularInline):
    model = Sensor
    readonly_fields = ["secret"]
    extra = 0


@admin.register(Corner)
class CornerAdmin(admin.ModelAdmin):
    inlines = [SensorInline]
    exclude = ["owner"]
    readonly_fields = ["score"]

    @admin.display(description="Wert (dBA)")
    def score(self, obj):
        return obj.score

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(CornerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.owner == request.user or request.user.is_superuser


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp"]

    @admin.display(description="Zeitstempel")
    def timestamp(self, obj):
        return obj.timestamp

    def get_queryset(self, request):
        qs = super(MeasurementAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sensor__corner__owner=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp"]

    @admin.display(description="Zeitstempel")
    def timestamp(self, obj):
        return obj.timestamp

    def get_queryset(self, request):
        qs = super(FeedbackAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(corner__owner=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser
