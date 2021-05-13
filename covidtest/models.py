from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.urls import reverse


# Vlastní vytvoření metody is_number, která se stará o kontrolu číselného vstupu ve znakovém poli.
# Využita je například u čísla pojištěnce, jelikož některá rodná čísla začínají 0.
def is_number(value):
    if not value.isdigit():
        raise ValidationError('Chybné číslo. Výskyt nečíselných znaků.')


class Osoba(models.Model):
    jmeno = models.CharField(max_length=100, verbose_name="Křestní jméno")
    prijmeni = models.CharField(max_length=100, verbose_name="Příjmení")
    datum_narozeni = models.DateField(help_text="Zadejte datum narození ve formátu <em>YYYY-MM - DD < / em >.",
                                      verbose_name="Datum narození")
    rodne_cislo = models.CharField(unique=True, max_length=10, validators=[is_number], verbose_name="Rodné číslo",
                                   help_text="Zadejte rodné číslo bez lomítka.")
    cislo_op = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(999999999)], verbose_name="Číslo OP")
    mesto = models.CharField(max_length=200, verbose_name="Město")
    ulice = models.CharField(max_length=220, verbose_name="Ulice včetně č. p.")
    # cislo_popisne = models.CharField(max_length=100, verbose_name="Číslo popisné")
    psc = models.PositiveIntegerField(validators=[MaxValueValidator(99999), MinValueValidator(10000)], verbose_name="PSČ")
    tel_cislo = models.PositiveIntegerField(validators=[MaxValueValidator(999999999), MinValueValidator(111111111)],
                                            verbose_name="Telefonní číslo")
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, verbose_name="E-mail")

    class Meta:
        ordering = ["prijmeni"]

    def __str__(self):
        return f'Jméno a příjmení: {self.jmeno} {self.prijmeni}, datum narození: {str(self.datum_narozeni)}, ' \
               f'rodné číslo: {self.rodne_cislo}'


class Pojistovna(models.Model):
    POJISTOVNY = (
        ('111 - VZP', '111 - VZP'),
        ('201 - Vojenská ZP ČR', '201 - Vojenská ZP ČR'),
        ('205 - ČPZP', '205 - ČPZP'),
        ('207 - OBZP', '207 - OBZP'),
        ('209 - ZP Škoda', '209 - ZP Škoda'),
        ('211 - ZPMVČR', '211 - ZPMVČR'),
        ('213 - RBP', '213 - RBP'),
    )
    pojistovna = models.CharField(max_length=20, choices=POJISTOVNY, default='111 - VZP', verbose_name="Zdravotní pojišťovna")

    def __str__(self):
        return f'Pojišťovna: {self.pojistovna}'


class Misto(models.Model):
    zemepisna_sirka = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)],
                                        verbose_name="Zeměpisná šířka")
    zemepisna_delka = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                        verbose_name="Zeměpisná délka")
    mesto = models.CharField(max_length=250, verbose_name="Město odběrného místa", null=True, blank=True)

    def __str__(self):
        return f'Zeměpisná šířka: {str(self.zemepisna_sirka)}, zeměpisná délka: {str(self.zemepisna_delka)}, město: {self.mesto}'


class Pojistenec(models.Model):
    cislo_pojistence = models.CharField(validators=[is_number], verbose_name="Číslo pojištěnce", max_length=10, unique=True)
    osoba = models.ForeignKey(Osoba, on_delete=models.CASCADE)
    zp = models.ForeignKey(Pojistovna, on_delete=models.CASCADE)

    class Meta:
        ordering = ["cislo_pojistence"]

    def __str__(self):
        return f'Číslo pojištěnce: {str(self.cislo_pojistence)}, {self.osoba}'


class Laborator(models.Model):
    nazev = models.CharField(verbose_name="Název laboratoře", max_length=200)

    class Meta:
        ordering = ["nazev"]

    def __str__(self):
        return f'Název laboratoře: {self.nazev}'


class Test(models.Model):
    navsteva = models.DateTimeField(auto_now_add=True, verbose_name="Čas návštěvy") # Zajistí aktuální časové razítko

    HODNOTY = (
        ("pozitivní", "pozitivní"),
        ("negativní", "negativní")
    )
    vyhodnoceni = models.CharField(max_length=9, choices=HODNOTY, verbose_name="Vyhodnocení testu")
    poznamka = models.TextField(blank=True, null=True, verbose_name="Poznámka")
    osoba = models.ForeignKey(Osoba, on_delete=models.CASCADE, verbose_name="Osoba")
    misto = models.ForeignKey(Misto, on_delete=models.CASCADE, verbose_name="Místo provedení testu")
    laborator = models.ForeignKey(Laborator, on_delete=models.CASCADE, verbose_name="Laboratoř")

    class Meta:
        ordering = ["-vyhodnoceni"]

    def __str__(self):
        return f'Navsteva: {str(self.navsteva)}, vyhodnoceni: {self.vyhodnoceni}, {self.osoba}'



