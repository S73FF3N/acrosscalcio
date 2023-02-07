from django.db import models


class ScoutingResult(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    playerSlug = models.CharField(max_length=200, db_index=True)
    initialSO5average15 = models.DecimalField(max_digits=4, decimal_places=1)
    initialFifthLastScore = models.DecimalField(max_digits=4, decimal_places=1)
    league = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    initialFloorPriceLimitedETH = models.DecimalField(max_digits=7, decimal_places=4)
    initialFloorPriceLimitedEUR = models.DecimalField(max_digits=7, decimal_places=2)
    not_for_sale = models.BooleanField(default=False)

    created = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.lastName:
            return self.lastName
        else:
            return self.firstName


class FloorPrice(models.Model):
    scouting_result = models.ForeignKey(ScoutingResult, default=1, on_delete=models.CASCADE, )
    floorPriceETH = models.DecimalField(max_digits=7, decimal_places=4)
    floorPriceEUR = models.DecimalField(max_digits=7, decimal_places=2)
    not_for_sale = models.BooleanField(default=False)

    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.scouting_result.__str__()