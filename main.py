from load_calculator_class import LoadCalculator


def main():
    load_calculator = LoadCalculator()
    load_calculator.load_pallets(*[0, 302, 189, 56, 78, 121, 0])
    load_calculator.calculate_load()
    trucks = load_calculator.trucks
    loose_pallets = load_calculator.loose_pallets

    print(f"{load_calculator.number_of_pallets} pallets, {load_calculator.number_of_trucks} trucks.")

    for i, truck in enumerate(trucks):
        print(f"\nTruck {i + 1} ({truck.number_of_pallets} pallets, {truck.total_ldm / 100} ldm):")
        for arrangement in truck.arrangements:
            print(arrangement)

    print(f"\nLoose pallets ({load_calculator.number_of_loose_pallets} pallets, {load_calculator.ldm_of_loose_pallets / 100} ldm):")
    for pallet in loose_pallets:
        print(pallet)


if __name__ == "__main__":
    main()
