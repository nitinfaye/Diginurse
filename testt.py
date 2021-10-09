from db.mongo import Person


x = Person("12355")

# x.save("new_treat")
# x.load()

r = x.load_round("123545")


print(r)