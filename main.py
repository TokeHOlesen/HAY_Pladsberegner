from load_calculator_class import LoadCalculator


def main():
    load_calculator = LoadCalculator()
    load_calculator.process()
    trucks = load_calculator.trucks
    loose_pallets = load_calculator.loose_pallets

    for i, truck in enumerate(trucks):
        print(f"\nTruck {i + 1} ({truck.total_ldm / 100} ldm):")
        for arrangement in truck.arrangements:
            print(arrangement)

    print("\nLoose pallets:")
    for pallet in loose_pallets:
        print(pallet)


if __name__ == "__main__":
    main()
