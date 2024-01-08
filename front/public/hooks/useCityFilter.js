import { useEffect, useState } from "preact/hooks"
import useCityPromotion from "./useCityPromotion";

export default function useCityFilter({ sourceList }) {
    const [ filteredList, setFilteredList ] = useState([]);
    const [ cityFilter, setCityFilter ] = useState("");
    const { cities, fetchCitiesWeekplan } = useCityPromotion();

    useEffect(() => {
        if (cityFilter === "" || cityFilter === null) {
            setFilteredList(sourceList);
            return
        }
        let newWp = sourceList.filter((e) => {
            return e.city === cityFilter
        });
        setFilteredList([...newWp]);
        console.log(filteredList, cityFilter);
    }, [ cityFilter, sourceList ]);

    const handleCityFilterChange = (event) => {
        setCityFilter(event.target.value);
    }

    return {
        filteredList: filteredList,
        cityFilter: cityFilter,
        setCityFilter: setCityFilter,
        handleCityFilterChange: handleCityFilterChange,
        cities: cities
    }
}