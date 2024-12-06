from typing import Sequence

from django.contrib.postgres.fields import ArrayField
from django.db.models import Func, F, Q, DateTimeField, When, Case, Value
from django.db.models.functions import Cast
from django_cte import With, CTEManager

from django_pg_rrule.fields import RruleField
from datetime import datetime


class RecurrenceManager(CTEManager):
    date_start_field = "date_start"
    date_end_field = "date_end"
    datetime_start_field = "datetime_start"
    datetime_end_field = "datetime_end"
    until_field = "rrule_until"

    def with_occurrences(
        self,
        start: datetime,
        end: datetime,
        start_qs: Q | None = None,
        additional_filter: Q | None = None,
        select_related: Sequence | None = None,
        prefetch_related: Sequence | None = None,
    ):
        """Evaluate rrules and annotate all occurrences."""

        start_qs = self if start_qs is None else start_qs

        with_qs = start_qs.filter(
            (
                Q(**{f"{self.datetime_start_field}__lte": end})
                | Q(**{f"{self.date_start_field}__lte": end.date()})
            )
            & (
                Q(**{f"{self.until_field}__isnull": True})
                | Q(**{f"{self.until_field}__gte": start})
            )
        )
        if additional_filter:
            with_qs = with_qs.filter(additional_filter)

        with_qs = with_qs.annotate(
            odatetime=Func(
                Case(
                    When(
                        condition=Q(rrule__isnull=False),
                        then=Func(
                            Func(
                                Cast("rrule", output_field=RruleField()),
                                F(self.datetime_start_field),
                                end,
                                function="get_occurrences",
                                output_field=DateTimeField(),
                            ),
                            F("rdatetimes"),
                            function="ARRAY_CAT",
                            output_field=ArrayField(DateTimeField()),
                        ),
                    ),
                    default=Func(
                        Value("{}", output_field=ArrayField(DateTimeField())),
                        F(self.datetime_start_field),
                        function="ARRAY_APPEND",
                        output_field=ArrayField(DateTimeField()),
                    ),
                ),
                function="UNNEST",
            ),
            odate=Func(
                Case(
                    When(
                        condition=Q(rrule__isnull=False),
                        then=Func(
                            Func(
                                Cast("rrule", output_field=RruleField()),
                                F(self.date_start_field),
                                end,
                                function="get_occurrences",
                                output_field=DateTimeField(),
                            ),
                            Cast("rdates", output_field=ArrayField(DateTimeField())),
                            function="ARRAY_CAT",
                            output_field=ArrayField(DateTimeField()),
                        ),
                    ),
                    default=Func(
                        Value("{}", output_field=ArrayField(DateTimeField())),
                        Cast(self.date_start_field, output_field=DateTimeField()),
                        function="ARRAY_APPEND",
                        output_field=ArrayField(DateTimeField()),
                    ),
                ),
                function="UNNEST",
            ),
        )
        cte = With(
            with_qs.only("id"),
            name="qodatetimes",
        )
        qs = (  # Join WITH clause with actual data
            cte.join(self.model, id=cte.col.id)
            .with_cte(cte)
            # Annotate WITH clause
            .annotate(odatetime=cte.col.odatetime, odate=cte.col.odate)
            # Exclude exdatetimes and exdates
            .exclude(
                (Q(odatetime__isnull=False) & Q(exdatetimes__contains=[F("odatetime")]))
                | (Q(odate__isnull=False) & Q(exdates__contains=[F("odate")]))
            )
            .filter(
                # With rrule, filter recurrences
                Q(
                    odatetime__lte=end,
                    odatetime__gte=start - (F("datetime_end") - F("datetime_start")),
                )
                | Q(
                    odate__lte=end.date(),
                    odate__gte=start.date() - (F("date_end") - F("date_start")),
                )
            )
        )

        if select_related:
            qs = qs.select_related(*select_related)

        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)

        # Hacky way to enforce RIGHT OUTER JOIN
        # Otherwise, Django always will rewrite the join_type to LEFT OUTER JOIN/INNER JOIN
        qs.query.alias_map["qodatetimes"].join_type = "RIGHT OUTER JOIN"

        return qs
