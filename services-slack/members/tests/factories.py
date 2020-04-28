import factory


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "members.Member"

    person_id = factory.Faker("uuid4")
